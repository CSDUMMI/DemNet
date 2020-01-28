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
                    , elections : List Election
                    , notices   : List String -- Short Messages for the user.
                    }

add_if_not_member : a -> List a -> List a
add_if_not_member element list
  = if List.member element list
    then list
    else element::list

remove_duplicates : List a -> List a
remove_duplicates list = List.foldl add_if_not_member [] list

save_page : Model -> Model
save_page model =
  case model.page of
    Reading message -> { model | readings = add_if_not_member message model.readings }
    Writing message -> { model | writings = add_if_not_member message model.writings }
    Feed messages   -> { model | feed =  remove_duplicates <| messages ++ model.feed }
    Vote election   -> { model | elections = add_if_not_member election }

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
  = let saved_model = save_page model
    in case msg of
      Writes writing_msg ->
        case saved_model.page of
          Writing message ->
            case writing_msg of
              Change field new ->
                  let new_message = case field of
                        Title -> { message | title = new }
                        Content -> { message | content = new }
                        To -> { message | to = new }
                  in ({ (save_page saved_model) | page = Writing new_message }, Cmd.none)
              Publish -> (model, publish message <| Published message)
          _ -> ( saved_model, Cmd.none )
      To_Feed             -> ( { saved_model | page = Feed saved_model.feed }, Cmd.none)
      Read other_message  -> ( { saved_model | page = Reading other_message }, Cmd.none)
      Write other_message -> ( { saved_model | page = Writing other_message }, Cmd.none)
      Saved message       -> ( { model | notices = ("Saved: " ++ message.title)::model.notices }, Cmd.none)
      Published message   -> ( { model | notices = ("Saved: " ++ message.title)::model.notices }, Cmd.none)
