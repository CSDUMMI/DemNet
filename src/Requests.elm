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

parseFetched : String -> List (Viewing.Post msg)
parseFetched fetched =
  -- Each Post is seperated by a line of #
  let parts = String.split "######################" fetched
      posts = List.map Viewing.stringToPost parts
  in posts
