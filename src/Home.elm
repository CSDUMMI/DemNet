module Home exposing (..)

import Cycle
import Time
import Viewing exposing (..)
import Html
import Element exposing (Element, text)
import Browser
import Element.Background as Background

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
                    , news : List (Viewing.Posting Msg)
                    }

news_ = [ Posting { title = "How to vote", content = Element.text "Hello, I'll introduce you to our voting scheme.\nIt is essentially the Alternative Vote or Instant-Run-Off Voting (IRV) "}
       , Posting { title = "Welcome to the Network", content = Element.text "Hello, we hope you'll join us" } ]

init : () -> (Model, Cmd Msg)
init _ = ( Model { cycle = Cycle.init "Democractic" ["Social", "Transperant" ]
                 , news = news_
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
view (Model model) =
  let description_adjective = Cycle.next model.cycle
      news = model.news
      body = Element.column [ Element.centerX, Element.alignTop ]
              [ (viewNavigation << News << Register << Login << Home ) None
              , text (description_adjective ++ " Network")
              , viewPosts news ]
  in  Element.layout [ Background.color Viewing.background_color ] body
