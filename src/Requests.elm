module Requests exposing ( save_post
                         , publish_post
                         , request_posts
                         , Post
                         , parsePosts
                         )

import Http

type alias Expect_Msg msg = ( Result Http.Error String -> msg )
type alias Post = { title : String
                  , content : String
                  , saved : Bool
                  , author : String
                  }

save_post : Expect_Msg msg -> Post -> Cmd msg
save_post = upload "save"

publish_post : Expect_Msg msg -> Post -> Cmd msg
publish_post = upload "publish"

upload : String -> Expect_Msg msg ->  Post -> Cmd msg
upload url expect { title, content }
  = Http.post { url = "/content/" ++ url
              , body = Http.stringBody "plain/text" ( "# " ++ title ++ "\n" ++ content)
              , expect = Http.expectString expect
              }

request_posts : Expect_Msg msg  -> Cmd msg
request_posts expect
  = Http.post { url = "/feed"
              , body = Http.emptyBody
              , expect = Http.expectString expect
              }

parsePosts : String -> List Post
parsePosts post_str
  = let single_posts = String.split "\n#########################################\n" post_str
    in List.filterMap stringToPost single_posts

stringToPost : String -> Maybe Post
stringToPost str_post =
    let ( title, author, content ) = case String.lines str_post of
          t::a::c -> ( t, a, c )
          t::c -> ( t, "", c )
          c -> ( "", "", c )
    in if title == "" || content == [] || author == ""
        then Nothing
        else Just { title = title
                  , content = String.join "\n" content
                  , author = author
                  , saved = True
                  }
