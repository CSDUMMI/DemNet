module News exposing (..)

import Viewing exposing (Nav_Items(..))
import Requests
import Http exposing ( Error (..) )
import Json.Decode exposing (Decoder, field, string)
import Browser
import Element
import Html

-- MAIN
main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- MODEL
type News
  = Success (List (Viewing.Posting Msg))
  | Loading
  | Failure String -- Error Message

type Model = Model { news : News }

init : () -> (Model, Cmd Msg)
init _ = ( Model { news = Loading }, Requests.fetchNews GotNews )


-- UPDATE

type Msg
  = GotNews (Result Http.Error String)
  | MoreNews


update : Msg -> Model -> (Model, Cmd Msg)
update msg (Model model) =
  case msg of
    GotNews result ->
      case result of
        Ok news -> (Model { model | news = Success (Requests.parseFetched news) }, Cmd.none)
        Err e ->
          case e of
            BadUrl url ->  (Model { model | news = (Failure "BadUrl" ++ url)} , Cmd.none)
            Timeout -> (Model { model | news = Loading }, Requests.fetchNews GotNews)
            NetworkError -> (Model { model | news = Loading }, Requests.fetchNews GotNews)
            BadStatus status -> (Model { model | news = Failure (Just (BadStatus status ))}, Requests.fetchNews GotNews)
            BadBody error -> (Model { model | news = Failure (Just (BadBody error)) }, Cmd.none)
    MoreNews -> (Model { model | news = Loading }, Requests.fetchNews GotNews)

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
view : Model -> Html.Html Msg
view (Model model) =
  let news_posts = case model of
       Success news -> Viewing.viewPosts news
       Loading -> Element.el Viewing.text_attr [Element.text "Loading"]
       Failure err ->
         case err of
           Just error -> Element.el Viewing.text_attr [Element.text "Error: " ++ (String.toString error)]
           Nothing -> Element.el Viewing.text_attr [Element.text "Error"]

      nav = (Viewing.viewNavigation << Register << Login << Home) None
  in Element.layout [Background.color background_color] Element.column [] (nav ++ news_posts)
