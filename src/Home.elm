module Home exposing (..)

import Cycle
import Time
import Viewing
import Html
import Element.Region as Region
import Browser

-- MAIN
main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- MODEL
type Model = Model  { cycle : Cycle.Cycle String
                    , news : List Viewing.Posting
                    }

init : () -> (Model, Cmd Msg)
init _ = ( Model { cycle = Cycle.init "Democractic" ["Social", "Transperant" ]
                 , news = []
                 }
         , Cmd.none )

-- UPDATE
type Msg = Change

update : Msg -> Model -> (Model, Cmd Msg)
update msg (Model model ) =
  case msg of
    Change -> (Model { model | cycle = Cycle.step model.cycle }, Cmd.none)

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Time.every 1000 (\_ -> Change)

-- VIEW
view : Model -> Html.Html Msg
view model =
  let description_adjective = Cycle.next model.cycle
  in Html.div []  [ viewNavigation
                  , Html.text description_adjective
                  , viewNews ]
