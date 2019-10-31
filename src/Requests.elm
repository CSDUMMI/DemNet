module Requests exposing  ( fetch
                          , fetchNews
                          , fetchPosts
                          , parseFetched
                          )

import Viewing
import Element exposing (text)
import Http

-- HTTP Requests and Parsing
fetch : String -> (Result Http.Error String -> msg) -> Cmd msg
fetch url msg =
  Http.post
    { url = url
    , body = Http.emptyBody
    , expect = Http.expectString msg }

fetchNews : (Result Http.Error String -> msg) -> Cmd msg
fetchNews = fetch "/news"

fetchPosts : ((Result Http.Error String -> msg) -> Cmd msg)
fetchPosts = fetch "/messages"

foldTwo_ : List (a,a) -> (a -> a -> (a,a) ) -> List a -> List (a,a)
foldTwo_ folded folding list =
  case list of
    [] -> folded
    [x] -> folded
    x::y::xs -> foldTwo_ ((folding x y)::folded) folding xs

foldTwo : (a -> a -> (a,a)) -> List a -> List (a,a)
foldTwo = foldTwo_ []

parseFetched : String -> List (Viewing.Posting msg)
parseFetched fetched =
  -- Tab Seperated Values
  let parts = String.split "\t" fetched
      parts_folded = foldTwo (\a b -> (a,b)) parts
      posts = List.map (\(title, content) -> Viewing.Posting { title = title, content = text content }) parts_folded
  in posts
