import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import (
    create_user,
    login_user,
    new_post,
    retrieve_user,
    list_posts,
    get_user_posts,
    get_post_by_id,
    list_tags,
    retrieve_tag,
    create_tag,
    new_category,
    list_categories,
    list_users,
    update_category,
    retrieve_category,
    update_tag,
    delete_tag
)


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
                    successfully_updated, status.HTTP_200_SUCCESS.value
                )

        elif url["requested_resource"] == "login":
            successfully_updated = login_user(request_body)
            if successfully_updated:
                return self.response(
                    successfully_updated, status.HTTP_200_SUCCESS.value
                )

        elif url["requested_resource"] == "posts":
            successfully_updated = new_post(request_body)
            if successfully_updated:
                return self.response(
                    successfully_updated, status.HTTP_200_SUCCESS.value
                )

        elif url["requested_resource"] == "categories":
            successfully_updated = new_category(request_body)
            if successfully_updated:
                return self.response(
                    successfully_updated, status.HTTP_200_SUCCESS.value
                )
        elif url["requested_resource"] == "tags":
            successfully_updated = create_tag(request_body)
            if successfully_updated:
                return self.response(
                    successfully_updated, status.HTTP_200_SUCCESS.value
                )
        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["query_params"]:
                user_id_list = url["query_params"]["user_id"]
                user_id = user_id_list[0]
                response_body = get_user_posts(user_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            if url["pk"] != 0:
                post_id = url["pk"]
                response_body = get_post_by_id(post_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_posts(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            if url["pk"] != 0:
                response_body = retrieve_tag(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                response_body = retrieve_category(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
    
            response_body = list_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)


    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response(successfully_updated, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = update_tag(pk, request_body)
                if successfully_updated:
                    return self.response(
                        successfully_updated, status.HTTP_200_SUCCESS.value
                    )
                else:
                    return self.response(
                        "Tag not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
            else:
                return self.response(
                    "Invalid tag ID", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
                )
        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )
 

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_deleted = delete_tag(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
           
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
