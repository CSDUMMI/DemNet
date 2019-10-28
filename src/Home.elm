module Home exposing (..)
import Browser
import Html exposing (..)
import Time
import Viewing exposing (..)
import Array

main = Browser.element
        {  init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }

descriptions =  Array.fromList
                [ "Democracy"
                , "DemNet"
                , "The democratic social network"
                ]

type alias Model = { description : Int }

init : () -> (Model, Cmd Msg)
init _ = { description = 0 }

type Msg = Change

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Change _ -> { model | description = if (length descriptions) > (description+1) then description + 1 else 0 }

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Time.every 1000 Change

view : Model -> Html Msg
view model =
  div []
    [ viewHeader
    , text [] [ Array.get description descriptions ]
    ]
