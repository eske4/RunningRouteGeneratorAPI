# Running Route Generator API

This API serves as a link between the OpenRouteService API and a Supabase-hosted database, providing various functionalities for the front-end application available [here](https://github.com/eske4/RunningRouteGeneratorClient).

## API Endpoints:

1. **/GetRoute/[lat]/[long]/[profile]/[route_pois]/**
   - Retrieves a route using the provided starting coordinates (`lat`, `long`) and a set of points of interest (`route_pois`). The `profile` parameter specifies the route profile.

2. **/GetPois/[lat]/[long]/**
   - Fetches nearby points of interest based on the given latitude (`lat`) and longitude (`long`).

3. **/GetPois/[lat]/[long]/[filter]/**
   -Similar to the previous command, with an additional filter to display specific categories of points of interest. Use IDs from OpenRouteService IDs found [here](https://github.com/GIScience/openpoiservice/blob/master/openpoiservice/server/categories/categories.yml).

4. **/GetIdList/[lat]/[long]/**
   - Obtains a list of all available IDs in the vicinity, representing different categories like parks, nature spots, shops, etc.

5. **/GetRandomIdList/[username]/[lat]/[long]/**
   - Executes an algorithm to recommend IDs based on user data stored in the Supabase database. Recommendations are influenced by user ratings and preferences.

6. **/SendRating/[username]/[catids]/[rating]/**
   - Uploads user ratings to the database, requiring a username, category IDs (`catids`), and a user rating.

The front-end application triggers these commands by sending requests to the API endpoint: `https://api-website.domain/`, followed by one of the 6 commands mentioned above.

## Example

An example of how a command are executed

**Input:**
your-domain-name.vercel.app/GetPois/56.717665/10.112082

**Output:**
```json
[
  ["Hadsund Tennesbaner", "288", "10.132055", "56.723234"],
  ["Hadsund Lystbaadehavn", "277", "10.105244", "56.709779"],
  ["Hadsund Fiskerihavn", "277", "10.125764", "56.716744"],
  ["Midtpunkt", "601", "10.112728", "56.717063"]
]
```

# Recreating the API

To recreate the API, follow these steps:

1. **Obtain an OpenRouteService API Key:**
   - Visit the [OpenRouteService website](https://openrouteservice.org/) to obtain an API key.

2. **Store repository:**
    - If you have Git installed, you can clone the repository using the following command:

    ```bash
    git clone https://github.com/eske4/RunningRouteGeneratorAPI.git
    ```

    Alternatively, you can download the project as a ZIP file:

   - Click on the "Code" button at the top of the repository.
   - Select "Download ZIP" from the dropdown menu.
   - After downloading, extract the contents to your desired location on your computer.

4. **Integrate OpenRouteService API Key:**
   - In the project, incorporate the obtained key into an environment variable named `api_key_ors` by assigning your OpenRouteService API key to it.
   - **Important:** When deploying publicly, avoid directly uploading sensitive keys. Instead, consider using environmental variables, as demonstrated in the code, to enhance security.

5. **Configure Supabase for Database Functionality:**
   - Create a Supabase account [here](https://supabase.com/).
   - In Supabase, create a project and a table named "UserData" with variables: `username`, `catid`, `count`, `rating`, `sum`. The SQL table creation script is provided below:

     ```sql
     CREATE TABLE public."UserData" (
       username text NOT NULL,
       catid bigint NOT NULL,
       count bigint NOT NULL,
       rating double precision NOT NULL,
       sum bigint NOT NULL,
       CONSTRAINT UserData_pkey PRIMARY KEY (username, catid),
       CONSTRAINT rating CHECK ((rating >= 0 AND rating <= 5))
     );
     ```

   - In the projects [to_database.py](scripts/to_database.py) and [predict_user.py](scripts/predict_user.py), within the `url=""` declaration, insert your Supabase URL. Additionally, create an environment variable named `api_key_supabase` and assign your Supabase API key to it. Obtain these details from your project settings under API settings in Supabase.
   - **Important:** When deploying publicly, avoid directly uploading sensitive keys. Instead, consider using environmental variables, as demonstrated in the code, to enhance security.

   If you do not wish to use the database functionality, you can comment out the relevant portions in [index.py](api/index.py) but is required for the client to work:
   - Remove or comment lines 5-6 and lines 45-60.

6. **Note: Library Versions and Code Adjustments:**
   - Please be aware that library versions might change over time. Make sure to check for updates and adjust the code accordingly.
   - If there are changes in library versions, some code modifications might be necessary to ensure compatibility. Keep an eye on the libraries' release notes for any breaking changes.

7. In [requirements.txt](requirements.txt), update Flask to the newest version.

8. Create a Vercel account and deploy the repository.
