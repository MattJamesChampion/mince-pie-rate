
using System;
using System.IO;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Azure.EventGrid.Models;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision.Models;
using Microsoft.Azure.EventGrid;
using System.Data.SqlClient;

namespace MincePieRate.Vision
{
    public static class ReadPieBoxDetails
    {
        private static readonly string subscriptionKey = Startup.Configuration["visionSubscriptionKey"];
        private static readonly string mincePieRateDB = Startup.Configuration["MincePieRateDB"];
        private const int numberOfCharsInOperationId = 36;

        [FunctionName("ReadPieBoxDetailsEG")]
        public static async Task<IActionResult> EventGridTest([EventGridTrigger]EventGridEvent eventGridEvent, ILogger log)
        {
            try
            {
                log.LogInformation("C# EventGrid Trigger function processed a request.");
                if (string.Equals(eventGridEvent.EventType, "Microsoft.Storage.BlobCreated", StringComparison.OrdinalIgnoreCase))
                {
                    log.LogInformation("C# EventGrid Trigger function processed a blob created request.");
                    var blobCreatedEvent = (StorageBlobCreatedEventData)eventGridEvent.Data;
                    var imageDetails = ExtractDetails(blobCreatedEvent.Url);

                    if (imageDetails.ImageType == "box_back_image")
                    {
                        var result = await ProcessImage(blobCreatedEvent.Url, log);
                        await UpdateMPRDB(await GetTextAsync(result.Item1, result.Item2, log), imageDetails);
                    }
                }
            }
            catch (Exception e)
            {
                log.LogError(e, "Error running image processing from event grid event.");
            }

            return new OkResult();
        }

        private static async Task UpdateMPRDB(string extractedText, ImageDetails details){
            //Pull out the file name and split it into its parts
            //Connect to MPR database
            //Uisng the PK of the row insert the text into the apporpirate column (also identified by the image file name)
            
            using(var con = new SqlConnection(mincePieRateDB)){
                await con.OpenAsync();
                var command = con.CreateCommand();
                command.CommandText = "UPDATE rate_mincepie set box_back_text = @boxText where id = @mpId";
                command.Parameters.AddWithValue("@boxText", extractedText);
                command.Parameters.AddWithValue("@mpId", details.MincePieId);
                await command.ExecuteNonQueryAsync();
            }
        }

        private static ImageDetails ExtractDetails(string imageURL){
            var uri = new Uri(imageURL);
            var parts = uri.LocalPath.Split(new string[]{"/"}, StringSplitOptions.RemoveEmptyEntries);
            var imageType = parts[1];
            var mincePieId = int.Parse(Path.GetFileNameWithoutExtension(parts[2]));

            return new ImageDetails{ImageType = imageType, MincePieId = mincePieId};
        }

        [FunctionName("ReadPieBoxDetails")]
        public static async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)]HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            var result = await ProcessImage(req.Query["imageUrl"], log);
            return (ActionResult)new OkObjectResult(await GetTextAsync(result.Item1, result.Item2,log));
        }

        public static async Task<Tuple<ComputerVisionClient, string>> ProcessImage(string imageUrl, ILogger log){
            ComputerVisionClient computerVision = new ComputerVisionClient(
                new ApiKeyServiceClientCredentials(subscriptionKey),
                new System.Net.Http.DelegatingHandler[] { }) {Endpoint="https://westeurope.api.cognitive.microsoft.com"};

            log.LogInformation("url: '" +imageUrl+"'");
            var textHeaders = await computerVision.RecognizeTextAsync(
                    imageUrl, TextRecognitionMode.Printed);

            return Tuple.Create(computerVision, textHeaders.OperationLocation);
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

    public class ImageDetails {
        public int MincePieId { get; set; }
        public string ImageType { get; set; }
    }
}