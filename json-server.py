import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
# from views import list_docks, retrieve_dock, delete_dock, update_dock
# from views import list_haulers, retrieve_hauler, delete_hauler, update_hauler
# from views import list_ships, retrieve_ship, delete_ship, update_ship, create_ship


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_POST(self):

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            successfully_updated = create_user(request_body)
            if successfully_updated:
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
