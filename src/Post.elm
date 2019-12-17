module Post exposing ( Post
                         , save
                         , publish
                         , fetch
                         , new
                         , decoder
                         , encode
                         )

import Http
import Json.Decode as D
import Json.Encode as E

type alias Expect_Msg msg = ( Result Http.Error String -> msg )
type alias Post = { saved : Bool
                  , title : String
                  , content : String
                  , author : String
                  }

save : Expect_Msg msg -> Post -> Cmd msg
save = upload "save"

publish : Expect_Msg msg -> Post -> Cmd msg
publish = upload "publish"

upload : String -> Expect_Msg msg ->  Post -> Cmd msg
upload url expect { title, content }
  = Http.post { url = "/content/" ++ url
              , body = Http.stringBody "plain/text" ( "# " ++ title ++ "\n" ++ content)
              , expect = Http.expectString expect
              }

fetch : Expect_Msg msg  -> Cmd msg
fetch expect
  = Http.post { url = "/feed"
              , body = Http.emptyBody
              , expect = Http.expectString expect
              }

new : String -> List Post
new str = case D.decodeString (D.list decoder) str of
  Ok ps -> ps
  Err _ -> []

decoder : D.Decoder Post
decoder =
  D.map3 (Post True)
    (D.field "title" D.string)
    (D.field "content" D.string)
    (D.field "author" D.string)

encode : Post -> E.Value
encode post =
  E.object
    [ ("title", E.string post.title)
    , ("content", E.string post.content)
    , ("author", E.string post.author)
    ]
