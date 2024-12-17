import com.microsoft.aad.msal4j.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Collections;
import java.util.concurrent.CompletableFuture;

public class PasswordlessPostgreSQL {

    // Azure AD App Details
    private static final String CLIENT_ID = "<YOUR_CLIENT_ID>";
    private static final String CLIENT_SECRET = "<YOUR_CLIENT_SECRET>";
    private static final String TENANT_ID = "<YOUR_TENANT_ID>";
    private static final String POSTGRES_SCOPE = "https://ossrdbms-aad.database.windows.net/.default";
    
    // PostgreSQL Connection Details
    private static final String DB_URL = "jdbc:postgresql://<YOUR_SERVER_NAME>.postgres.database.azure.com:5432/<YOUR_DATABASE_NAME>";

    public static void main(String[] args) {
        try {
            // Fetch Access Token from Azure AD
            String accessToken = getAccessToken();
            System.out.println("Access Token: " + accessToken);

            // Connect to PostgreSQL using the Token
            Connection connection = connectToPostgreSQL(accessToken);
            if (connection != null) {
                System.out.println("Successfully connected to PostgreSQL using passwordless authentication!");
                connection.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Fetch Access Token using MSAL4J
    private static String getAccessToken() throws Exception {
        ConfidentialClientApplication app = ConfidentialClientApplication.builder(
                CLIENT_ID,
                ClientCredentialFactory.createFromSecret(CLIENT_SECRET))
                .authority("https://login.microsoftonline.com/" + TENANT_ID)
                .build();

        ClientCredentialParameters parameters = ClientCredentialParameters.builder(
                Collections.singleton(POSTGRES_SCOPE))
                .build();

        CompletableFuture<IAuthenticationResult> future = app.acquireToken(parameters);
        IAuthenticationResult result = future.get();
        return result.accessToken();
    }

    // Connect to PostgreSQL using Access Token
    private static Connection connectToPostgreSQL(String accessToken) throws SQLException {
        DriverManager.registerDriver(new org.postgresql.Driver());

        // Use the token as the password in the JDBC connection
        String connectionString = DB_URL + "?sslmode=require";
        return DriverManager.getConnection(connectionString, "azure_user@<YOUR_SERVER_NAME>", accessToken);
    }
}
