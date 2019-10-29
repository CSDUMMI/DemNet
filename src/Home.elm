module Home exposing (..)
import Browser
import Html exposing (..)
import Time
import Viewing exposing (..)
import Array
import Delay
import Cycle

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

type alias Model =  { cycle : Cycle.Cycle String }

init : () -> (Model, Cmd Msg)
init _ = ({ cycle = Cycle.init "Democratic"
                [ "Transparent"
                , "Free"
                , "Libre"
                , "The democratic social network"
                ]
         }, Cmd.none )
type Msg = Change

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Change -> ({ model | cycle = Cycle.step model.cycle }, Cmd.none )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Time.every 4000 (\_ -> Change)

view : Model -> Html Msg
view model =
  div []
    [ viewHeader
    , text (Cycle.next model.cycle)
    ]
