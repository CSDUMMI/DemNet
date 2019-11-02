module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Url
import Array

import Element exposing ( Element
                        , text
                        , row
                        )
import Element.Background as Background

import Requests
import Cycle

-- MAIN
main = Browser.application
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  , onUrlRequest = LinkClicked
  , onUrlChange = UrlChanged
  }

-- MODEL
type alias Model
  = { main_page : Main_Page
    , navigation : Nav_Items
    }

-- UPDATE
type Msg
  = Save_Post Post.Post
  | Change_Main_Page Main_Page
  | Writing_Publish
  |
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
  , body = Element.layout [] [Element.text "Hello"]
  }
