module Main exposing (..)

import Browser
import Array

import Element exposing ( Element
                        , text
                        , row
                        )
import Element.Background as Background

import Requests

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
            Title -> ( { p | title = post_element }, Cmd.none )
            Content -> ( { p | content = post_element }, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Upload kind post ->
      case model of
        Writing p ->
          let new_cmd = case kind of
                  Publish -> Requests.publish_post post
                  Save -> Requests.save_post post
          in (model,new_cmd)
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Switch_To_Feed ->
      case model of
        Writing p -> ( Feed [], Requests.request_posts Recv_Posts )
        Reading p -> ( Feed [], Request.request_posts Recv_Posts )
        Feed ps   ->  ( Feed ps, Requests.request_posts Recv_Posts )

    Recv_Posts posts ->
      case model of
        Writing p -> ( Writing p, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps   -> ( Feed ( ( Requests.parsePosts posts ) ++ ps ), Cmd.none )
