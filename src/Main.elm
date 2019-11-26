module Main exposing (..)

import Browser
import Array
import Http
import Html
import Requests exposing ( Post )

-- MAIN
main = Browser.element
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  }

-- MODEL
type Model
  = Reading Post
  | Writing Post
  | Feed (List Post)

init : flags ->  ( Model, Cmd Msg )
init _ = ( Feed [], Cmd.none )


-- UPDATE
type Post_Element = Title | Content

type Upload_Type = Publish | Save

type Msg
  = Read Post -- Switch to Reading with this Post
  | Write Post -- Writing with the Writing with this post
  | Changed  Post_Element String -- Change data structure accordingly
  | Upload Upload_Type Post
  | Saved ( Result Http.Error String )
  | Switch_To_Feed -- Go to Feed
  | Recv_Posts String

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Read post ->
      case model of
        Writing p -> ( Writing p, Cmd.none )
        Reading p -> ( Reading post, Cmd.none )
        Feed ps -> ( Reading post, Cmd.none )

    Write post ->
      case model of
        Writing p -> ( Writing  p, Cmd.none )
        Reading p -> ( Writing post, Cmd.none )
        Feed ps -> ( Writing post, Cmd.none )

    Changed element post_element ->
      case model of
        Writing p ->
          case element of
            Title -> ( { p | title = post_element, saved = False }, Cmd.none )
            Content -> ( { p | content = post_element, saved = False }, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Upload kind post ->
      case model of
        Writing p ->
          let new_cmd = case kind of
                  Publish -> Requests.publish_post post Saved
                  Save -> Requests.save_post post Saved
          in (model,new_cmd)
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Saved result ->
      case model of
        Writing p -> case result of
          Ok response -> ( Writing { p | saved = ( response == "Posted" ) }, Cmd.none )
          Err err -> ( Writing { p | saved = False }, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Switch_To_Feed ->
      case model of
        Writing p -> case p.saved of
          True -> ( Feed [], Requests.request_posts Recv_Posts )
          False -> ( Writing p, Requests.save_post Saved p )
        Reading p -> ( Feed [], Requests.request_posts Recv_Posts )
        Feed ps   ->  ( Feed ps, Requests.request_posts Recv_Posts )

    Recv_Posts posts ->
      case model of
        Writing p -> ( Writing p, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps   -> ( Feed ( ( Requests.parsePosts posts ) ++ ps ), Cmd.none )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
view : Model -> Html Msg
view model =
