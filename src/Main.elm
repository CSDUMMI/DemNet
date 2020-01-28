module Main exposing (..)
{-| DemNet Frontend
-}
import Browser
import Element exposing (Element)
import Http

main = Browser.element  { init = init
                        , view = view
                        , update = update
                        , subscription = subscription
                        }

-- MODEL
type alias User = { username : String
                  , first_name : String
                  , last_name : String
                  }

type alias Message
  = { from : User
    , to : User
    , title : String
    , content : String
    }

type Page
  = Reading Message
  | Writing Message
  | Feed (List Message)
  | Vote Election

type alias Model =  { user      : User
                    , page      : Page
                    , readings  : List Message
                    , writings  : List Message
                    , feed      : List Message
                    , notices   : List String -- Short Messages for the user.
                    }

init : flags -> ( Model, Cmd Msg)
init _ = ( { user = Nothing
           , readings = []
           , writings = []
           , feed = []
           }, Cmd.none )

-- UPDATE
type Msg
  = Writes Writing_Msg
  | To_Feed
  | Read Message
  | Write Message
  | Saved Message
  | Published Message

type Writing_Msg
  = Change Field String
  | Publish

type Field
  = Title
  | Content
  | To

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model
  = case model.page of
    Writing message ->
      case msg of
        Writes writing_msg ->
          case writing_msg of
            Change field new ->
              let new_message = case field of
                Title -> { message | title = new }
                Content -> { message | content = new }
                To -> { message | to = new }
              in ({ model | page = Writing new_message }, Cmd.none)
            Publish -> (model, publish message <| Published message)
        To_Feed -> ( { model | page = Feed model.feed, writings = remove_duplicates <| model.writings ++ message }, save message (Saved message))
