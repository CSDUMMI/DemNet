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
type Post = Post  { title : String
                  , content : String -- Markdown
                  }

type alias User = { img_src : String
                  , first_name : String
                  , last_name : String
                  }

type Main_Page
  = Feed  {  messages : Array.Array Post
          }
  | Writing { post : Post
            }
  | Reading { message : Post
            }

type Actions
  = Publish_Post Actions { onClick : Msg }
  | Create_Post Actions { onClick : Msg }
  | No_Action

type Nav_Items
  = Home Nav_Items
  | Register Nav_Items
  | Login Items
  | No_Nav_Item

type Model
  = Model { navigation : Nav_Items
          , user : Maybe User
          , main_page : Main_Page
          , actions : Actions
          }

-- Landing Page settings
init : () -> Url.Url -> Nav.Key -> Model
init flags url key = Model  { navigation = (Register << Login << Home) None
                            , user = Nothing
                            , key = key
                            , url = url
                            , title = "DemNet"
                            , main_page = Feed { messages = Array.empty }
                            , actions = No_Action
                            }
-- UPDATE
type Msg
  = Feed_Message_Clicked Int
  | Publish_Request
  | Create_Post_Request

  | Writing_Title_Changed String -- Save the post on server
  | Writing_Content_Changed String -- Save the post on server

  | UrlChanged Url.Url
  | LinkClicked Browser.UrlRequest

update : Msg -> Model -> Model
update msg model =
  case msg of

    UrlChanged url -> ( { model | url = url }, Cmd.none )

    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    Feed_Message_Clicked message_id ->
      case model.main_page of
        Feed messages ->
          let message = case Array.get message_id messages of
                Just m -> m
                Nothing -> emptyPost -- Feed will redirect to Feed.
          in (if message == emptyPost then ( model, Cmd.none ) else 





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
