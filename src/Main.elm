module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Url
import Array

import Element exposing ( Element
                        , text
                        , row
                        )
import Element.Background as Background

import Requests
import Cycle

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
type Msg
  = Read Post -- Switch to Reading with this Post
  | Write Post -- Writing with the Writing with this post
  | Writing_Title String -- Write Title to Data Type
  | Writing_Content String -- Write Content to Data Type
  | Save_Writing
  | Switch_To_Feed -- Go to Feed

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Read post ->
      case model of
        Writing p -> ( Write p, Cmd.none )
        Reading p -> ( Reading post, Cmd.none )
        Feed ps -> ( Reading post, Cmd.none )

    Write post ->
      case model of
        Writing p -> ( Writing  p, Cmd.none )
        Reading p -> ( Writing post, Cmd.none )
        Feed ps -> ( Writing post, Cmd.none )

    Writing_Title title ->
      case model of
        Writing p -> ( Writing (Post { p | title = title }), Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Writing_Content content ->
      case model of
        Writing p -> ( Writing (Post { p | content = content }), Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Save_Writing ->
      case model of
        Writing p -> ( Writing p, Requests.save_post p)
