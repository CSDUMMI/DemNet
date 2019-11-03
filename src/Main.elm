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
  = Read Post
  | Writing_Title String
  | Switch_To_Feed

update : Msg -> Model -> ( Model, Cmd Msg ) 
