module Post exposing  ( Post
                      , emptyPost
                      , toString
                      )

type Post = Post  { title : String
                  , content : String -- Markdown
                  }

opts =      { githubFlavored = Just { tables = True, breaks = True }
            , defaultHighlighting = Just "elm"
            , sanitize = True
            , smartypants = True
            }

-- Interpret the first #1 Heading as the title, and use anything else as content
stringToPost : String -> Post msg
stringToPost str_post =
  let post_lines = String.lines  str_post
      title_ = List.head (List.filter (\t -> String.startsWith "# " t) post_lines)
      title =
        case title_ of
          Just t -> t
          Nothing -> ""

      content_lines = List.filter ((/=) title) post_lines
      content = (Element.html << (toHtmlWith opts []) << (String.join "\n")) content_lines
  in  Post { title = title, content = content }


parsePosts : String -> List (Post.Post msg)
parsePosts posts =
  -- Each Post is seperated by a line of #
  let parts = String.split "\n######################\n" posts
      -- If you want to write this specific line in your post, use this line:
      parts_ =  List.map (String.replace "\n\\######################\n" "\n######################\n") parts
      posts = List.map stringToPost parts_
  in posts

toString : Post -> String
toString (Post { title, content }) = (String.concat [ "# ", title ]) ++ content
