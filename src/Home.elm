module Home exposing (..)
import Browser
import Element
import Time
import Viewing exposing (..)
import Array
import Delay
import Cycle
import Html

main = Browser.element
        {  init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }

type alias Model =  { cycle : Cycle.Cycle String
                    , news : List Posting
                    }

init : () -> (Model, Cmd Msg)
init _ = ({ cycle = Cycle.init "Democratic"
                [ "Transparent"
                , "Free"
                , "Libre"
                , "The democratic social network"
                ]
          , news =  [ Posting { title = "Welcome", content = Text "We welcome you to DemNet" }
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

view : Model -> Html.Html Msg
view model =
  let element = Element.column []
                  [ viewHeader
                  , Element.text (Cycle.next model.cycle)
                  , viewPosts model.news
                  ]
  in Element.layout [] element
