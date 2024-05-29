import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import create_user, login_user


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for rare publishing"""

    def do_POST(self):

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            successfully_updated = create_user(request_body)
            if successfully_updated:
                return self.response(
                    successfully_updated, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                )

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
