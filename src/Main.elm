module Main exposing

import Browser
import Http
import Html
import Element as E
import Element.Events as Events
import Element.Border as Border
import Element.Input as Input
import Json.Decode as D

import Post exposing ( Post )
import Views exposing ( Post_Element (..), Upload_Type (..))
import RemovingCache exposing (RemovingCache)
import User exposing ( User )

-- MAIN
main : Program () Model Msg
main = Browser.element
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  }

-- MODEL
type Model
  = Authorized Authorized_Model
  | Unautherized Unautherized_Model

type alias Authorized_Model = { state : State
                              , storage : Storage
                              , user : User
                              }

type State
  = Reading Post
  | Writing Post
  | Feed (List Post)

type alias Storage = { readings : List Post
                     , writings : List Post
                     , feed : List Post
                     }

type alias Unautherized_Model = { state : Unautherized_State }

type alias Unautherized_State = { username : String
                                , password : String
                                , email : String
                                }

{-| Save a State in the Storage of an Authorized_Model.
-}
save_in : State -> Authorized_Model -> Authorized_Model
save_in state auth_model
  = let storage = auth_model.storage
    in case state of
      Reading p -> { auth_model | storage = { storage | readings = p::storage.readings } }
      Writing p -> { auth_model | storage = { storage | writings = p::storage.writings } }
      Feed ps -> { auth_model | storage = { storage | feed = ps ++ storage.feed }}

{-| Less general version of save_in, using the current state of a Authorized_Model and saves that
-}
save : Authorized_Model -> Authorized_Model
save auth_model = save_in auth_model.state auth_model

{-| Change the State from Authorized_Model to another one.
-}
change_state : Authorized_Model -> State -> Model
change_state auth_model new_state = let new_model = save auth_model
                                    in Authorized new_model

init : flags -> (Model, Cmd Msg)
init _ = (Unautherized { state =  { username = ""
                                  , password = ""
                                  , email = ""
                                  }
                       }, Cmd.none)
-- UPDATE
type Msg
  = Authorized_Msgs Authorized_Msg
  | Unauthorized_Msgs Unauthorized_Msg

type Authorized_Msg
  = Read Post
  | Write Post
  | Write_Enter Views.Post_Element String
  | Switch_To_Feed
  | Recv_Posts (Result Http.Error (List Post))

type Login_Field = Username | Password | Email

type Unauthorized_Msg
  = Login
  | Login_Enter Login_Field String
  | Login_Response (Result Http.Error Bool)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case model of

    Authorized auth_model ->
      case msg of
        Authorized_Msgs auth_msg ->
          case auth_msg of
            Read p -> (change_state auth_model <| Reading p)
            Write p -> (change_state auth_model <| Writing p)
            Write_Enter field value ->
              case auth_model.state of
                Reading p -> (model, Cmd.none)
                Writing p -> case field of
                  Views.Title -> (Authorized <| { auth_model | state = Writing { p | title = value }}, Cmd.none)
                  Views.Content -> (Authorized <| { auth_model | state = Writing { p | content = value }}, Cmd.none)
                Feed ps -> (model, Cmd.none)
            Switch_To_Feed -> (change_state auth_model <| Feed auth_model.storage.feed, Post.fetch Recv_Posts)
            Recv_Posts response ->
              case response of
                Ok ps -> (Authorized <| save_in (Feed ps) auth_model, Cmd.none)
                Err error -> (model, Cmd.none)
        Unauthorized_Msgs unauth_msg -> (model, Cmd.none)

    Unautherized unauth_model ->
      case msg of
        Authorized_Msgs auth_msg -> (model, Cmd.none)
        Unauthorized_Msgs unauth_msg ->
          case unauth_msg of
            Login -> let state = unauth_model.state
                     in (model, User.login state.username state.password state.email)
            Login_Enter field value -> let state = unauth_model.state
                                           new_state = case field of
                                             Username -> { state | username = value }
                                             Password -> { state | password = value }
                                             Email -> { state | email = value }
                                       in (Unautherized { state = state }, Cmd.none)

            Login_Response response ->
              case response of
                Ok user -> let new_model = Authorized  { state = Feed []
                                                       , storage = { readings = []
                                                                   , writings = []
                                                                   , feed = []
                                                                   }
                                                       , user = user
                                                       }
                           in if user == User.empty then (model, Cmd.none) else (new_model, Cmd.none)
                Err error -> (model, Cmd.none)

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
view : Model -> Html.Html Msg
view model =
  let page = case model of
        Unautherized unauth_model ->
          [ Input.username [] { onChange = Login_Enter Username
                              , text = "Username"
                              , placeholder = Nothing
                              , label = Input.labelLeft [] <| E.text "Username"
                              }
          , Input.currentPassword [] { onChange = Login_Enter Password
                                     , text = "Password"
                                     , placeholder = Nothing
                                     , label = Input.labelLeft [] <| E.text "Password"
                                     , show = False
                                     }
          , Input.button [] { onPress = Just Login
                            , label = E.text "Login"
                            }
          ]
        Authorized auth_model ->
          case auth_model.state of
            Reading p -> Views.reading p
            Writing p -> Views.writing p
            Feed ps   -> Views.feed ps
  in E.layout [E.centerX]
      <| E.column [] page
