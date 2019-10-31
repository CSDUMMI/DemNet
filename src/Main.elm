module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Url
import Element exposing ( Element
                        , text
                        , row
                        )
import Element.Background as Background
import Viewing
import Requests
import Cycle

-- MAIN
main = Browser.application
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  , onUrlRequest = onUrlRequest
  , onUrlChange = onUrlChange
  }

-- MODEL

type Model = Model
  { navigation : Viewing.Nav_Items
  , user : Maybe Viewing.User
  , messages : List (Viewing.Post Msg)
  , key : Nav.Key
  , url : Url.Url
  , title : String -- Page Title
  , main_page : Viewing.Main_Page -- Use of the current Main Page
  , actions : Viewing.Actions --- All possible Action Buttons
  }


-- UPDATE
type Msg
  = EnterPassword

update : Msg -> Model -> Model
update

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
-- views:
-- NavBar (Different Nav_Items, depending on the Context )
-- User ( User's Name and Image )
-- Feed ( Feed of Messages send to the user )
-- Actions (Actionsbar on the right side, a collection of actions, such as edit, publish, logout, etc.)
-- Editing (Edit and publish a Post)
-- Reading (Read a Post)
-- Login
-- Register

view : Model -> Browser.Document Msg
view (Model model) =
  { title = model.title
  , body = Element.layout []
            (Element.column []
              [ viewNavBar navigation
              , viewUser model.user
              , viewMainPage model.main_page
              , viewActions]
