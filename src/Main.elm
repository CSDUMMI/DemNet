module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Url
import Element exposing ( Element
                        , text
                        , row
                        )
import Element.Background as Background
import Viewing exposing ( viewUser
                        , viewMainPage
                        , viewActions
                        , viewHeadBar
                        , Nav_Items (..)
                        , Main_Page (..)
                        , Actions (..)
                        )
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

type Model = Model
  { navigation : Viewing.Nav_Items
  , user : Maybe Viewing.User
  , messages : List (Viewing.Post Msg)
  , key : Nav.Key
  , url : Url.Url
  , title : String -- Page Title
  , main_page : Viewing.Main_Page Msg -- Use of the current Main Page
  , actions : Viewing.Actions Msg--- All possible Action Buttons
  }

-- Landing Page settings
init : () -> Url.Url -> Nav.Key -> Model
init flags url key = Model  { navigation = (Register << Login << Home) None
                            , user = Nothing
                            , messages = []
                            , key = key
                            , url = url
                            , title = "DemNet"
                            , main_page = Login_Page
                            , actions = No_Action
                            }
-- UPDATE
type Msg
  = ChangedPassword String
  | ChangedUsername String
  | Login_Requested
  | UrlChanged Url.Url
  | LinkClicked Browser.UrlRequest

update : Msg -> Model -> Model
update msg model =
  case msg of
    ChangedPassword password ->
      let new_user = case model.user of

    ChangedUsername _ -> (model, Cmd.none)
    Login_Requested -> model
    UrlChanged url -> ( { model | url = url }, Cmd.none )
    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )



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
