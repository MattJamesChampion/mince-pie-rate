
using System;
using Microsoft.Extensions.Configuration;

namespace MincePieRate.Vision
{
    public class Startup
    {
        public static IConfigurationRoot Configuration;

        static Startup()
        {
            string env = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT");

            if (string.IsNullOrWhiteSpace(env))
            {
                env = "Development";
            }

            var builder = new ConfigurationBuilder();

            if (env == "Development")
            {
                builder.AddUserSecrets<Startup>();
            }

            Configuration = builder.Build();
        }
    }
}
