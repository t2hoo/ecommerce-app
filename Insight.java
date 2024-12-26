import org.apache.log4j.Logger;

public class Log4jXmlWithAppInsights {
    private static final Logger logger = Logger.getLogger(Log4jXmlWithAppInsights.class);

    public static void main(String[] args) {
        // Log messages at different levels
        logger.info("Application started.");
        logger.debug("Debugging information.");
        logger.warn("This is a warning message.");
        logger.error("This is an error message.");

        try {
            throw new Exception("Simulated Exception");
        } catch (Exception e) {
            logger.error("Exception occurred", e);
        }

        logger.info("Application finished.");
        System.out.println("Logs sent to Azure Application Insights.");
    }
}
