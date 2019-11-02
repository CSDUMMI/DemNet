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
type alias User = { img_src : String
                  , first_name : String
                  , last_name : String
                  }

type Main_Page
  = Feed  {  messages : Array.Array Post.Post
          }
  | Writing { post : Post.Post
            , saved : Bool
            }
  | Reading { message : Post.Post
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

  | Saved (Result Http.Error String)

  | UrlChanged Url.Url
  | LinkClicked Browser.UrlRequest

switchToWriting : Model -> Model
switchToWriting (Model model) = Model { model | main_page = Writing Post.emptyPost }

update : Msg -> Model -> Model
update msg (Model model)  =
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
              m_id_str = String.fromInt messages
              url = Nav.pushUrl model.key (Builder.absolute [ "message" ] [])
          in (if message == emptyPost
              then ( model, Cmd.none )
              else ( Model { model | main_page = Reading { message = message } }, url )
              )

        Writing _ -> (model, Cmd.none) -- Do Nothing
        Reading _ -> (model, Cmd.none)

    Publish_Request ->
      case model.main_page of
        Feed _ -> (model, Cmd.none)
        Writing { post } -> ( model, Requests.publishPost post )
        Reading _ -> ( model, Cmd.none )

    Create_Post_Request ->
      let url = Builder.absolute [ "writing" ]
      in (case model.main_page of
          Feed _ -> ( switchToWriting model, Nav.pushUrl model.key url )
          Reading _ -> ( switchToWriting model, Nav.pushUrl model.key url )
          Writing { post } -> ( model, Cmd.none )
         )

    -- Change Title and save on server
    Writing_Title_Changed title ->
      case model.main_page of
        Writing (Post post) ->
          let changed_post = { post | title = title }
              save_request = Requests.save_post Saved_Title changed_post
          in ( Model { model | main_page = Writing (Post changed_post) }, save_request )

        Reading _ -> ( model, Cmd.none )
        Feed _ -> ( model, Cmd.none )

    Writing_Content_Changed content ->
      case model.main_page of
        Writing { post } ->
          let changed_post = Post { post | content = content }
              save_request = Requests.save_post Saved_Content changed_post
          in ( Model { model | main_page = Writing (Post changed_post) }, save_request )

        Reading _ -> ( model, Cmd.none )
        Feed _ -> ( model, Cmd.none )

    Saved result ->
      case model.main_page of
        Writing (Post post)


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
