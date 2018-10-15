
using System;
using System.IO;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision.Models;

namespace MincePieRate.Vision
{
    public static class ReadPieBoxDetails
    {
        private static readonly string subscriptionKey = Startup.Configuration["visionSubscriptionKey"];
        private const int numberOfCharsInOperationId = 36;

        [FunctionName("ReadPieBoxDetails")]
        public static async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)]HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            ComputerVisionClient computerVision = new ComputerVisionClient(
                new ApiKeyServiceClientCredentials(subscriptionKey),
                new System.Net.Http.DelegatingHandler[] { }) {Endpoint="https://westeurope.api.cognitive.microsoft.com"};

            var imageUrl = req.Query["imageUrl"];
            log.LogInformation("url: '" +imageUrl+"'");
            var textHeaders = await computerVision.RecognizeTextAsync(
                    imageUrl, TextRecognitionMode.Printed);

            return (ActionResult)new OkObjectResult(await GetTextAsync(computerVision, textHeaders.OperationLocation,log));
        }

        private static async Task<string> GetTextAsync(
            ComputerVisionClient computerVision, string operationLocation, ILogger log)
        {
            // Retrieve the URI where the recognized text will be
            // stored from the Operation-Location header
            string operationId = operationLocation.Substring(
                operationLocation.Length - numberOfCharsInOperationId);

            Console.WriteLine("\nCalling GetTextRecognitionOperationResultAsync()");
            TextOperationResult result =
                await computerVision.GetTextOperationResultAsync(operationId);

            // Wait for the operation to complete
            int i = 0;
            int maxRetries = 60;
            while ((result.Status == TextOperationStatusCodes.Running ||
                    result.Status == TextOperationStatusCodes.NotStarted) && i++ < maxRetries)
            {
                Console.WriteLine(
                    "Server status: {0}, waiting {1} seconds...", result.Status, i);
                await Task.Delay(1000);

                result = await computerVision.GetTextOperationResultAsync(operationId);
            }//TODO make the method of waiting less rubbish, maybe use durable function?

            if(result.RecognitionResult == null && result.Status != TextOperationStatusCodes.Failed) {
                log.LogError("Failed to OCR text from image. Max try count exceeded.");
                return null;
            }

            if(result.Status == TextOperationStatusCodes.Failed) {
                log.LogError("Failed to OCR text from image.");
                return null;
            }

            return string.Join(Environment.NewLine, result.RecognitionResult.Lines.Select(l => l.Text));
        }
    }
}