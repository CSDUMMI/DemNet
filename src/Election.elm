module Election exposing (Election, vote, options, save)
{-| Representation of holding an election.
Enables you to vote, see your options and save your vote on the server.
# Definition
@docs Election
# Voting
@docs vote, options
# Networking
@docs save
-}

import Element as E
import Markdown

{-| An Election has many data points. All of them are held in here.
-}
type alias Election = { closes : Time.Posix
                      , options : List Option
                      , description : String -- Markdown
                      , title : String
                      , vote : List Option
                      }

{-| An Option is a something you can vote for
-}
type alias Option = { title : String
                    , description : String -- Markdown
                    , index : Int
                    }

{-| Function to view a short summary of the vote
-}
view_short_election : (Time.Month -> String) -> Time.Zone -> Election -> Element msg
view_short_election monthToString dayToString zone election
  = let date = Time.toMonth zone election.closes
               |> monthToString
               |> (++) "/"
               |> Time.toDay zone election.closes
               |> Debug.toString
               |> (++) "/"
               |> (++) Time.toYear zone election.closes
               |> Debug.toString
