module Main exposing (..)
{-| DemNet Frontend
-}
import Browser
import Element exposing (Element)
import Http

main = Browser.document { init = init
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

type alias Model =  { user      : Maybe User
                    , page      : Page
                    , readings  : List Message
                    , writings  : List Message
                    , feed      : List Message
                    }

init : flags -> ( Model, Cmd Msg)
init _ = ( { user = Nothing
           , readings = []
           , writings = []
           , feed = []
           }, Cmd.none )

-- UPDATE
type Msg
  = Read Message
  | Write Message
  | Feed
  | Write_Change_Title String
  | Write_Change_Content String
  | Login_Username_Change String
  | Login_Password_Change String

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model
  = case model.user of
      Just user -> case msg of
        Read msg ->
      Nothing   ->
