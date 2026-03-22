# Auth flow

Login → `create_access_token()`

`↓`

Client receives JWT

`↓`

Authorization: Bearer <token>
   
 `↓`

`oauth_scheme` extracts token

`↓`

`get_current_user()`

`↓`

`verify_access_token()`

