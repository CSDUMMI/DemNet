module Main exposing (..)

import Browser
import Array
import Http
import Html
import Element
import Json.Decode as D

import Post exposing ( Post )
import Views exposing ( Post_Element (..), Upload_Type (..))

-- MAIN
main : Program () Model Msg
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
init _ = ( Feed [], Post.fetch Recv_Posts )


-- UPDATE
type Msg
  = Read Post -- Switch to Reading with this Post
  | Write Post -- Writing with the Writing with this post
  | Changed  Post_Element String -- Change data structure accordingly
  | Upload Upload_Type Post
  | Saved ( Result Http.Error String )
  | Switch_To_Feed -- Go to Feed
  | Recv_Posts ( Result Http.Error String )

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
          let post = case element of
                Title -> { p | title = post_element, saved = False }
                Content -> { p | content = post_element, saved = False }
          in ( Writing post, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps -> ( Feed ps, Cmd.none )

    Upload kind post ->
      case model of
        Writing p ->
          let new_cmd = case kind of
                  Publish -> Post.publish Saved post
                  Save -> Post.save Saved post
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
          True -> ( Feed [], Post.fetch Recv_Posts )
          False -> ( Writing p, Post.save Saved p )
        Reading p -> ( Feed [], Post.fetch Recv_Posts )
        Feed ps   ->  ( Feed ps, Post.fetch Recv_Posts )

    Recv_Posts posts ->
      case model of
        Writing p -> ( Writing p, Cmd.none )
        Reading p -> ( Reading p, Cmd.none )
        Feed ps   ->
          ( case posts of
              Ok new_posts -> Feed ((Post.new new_posts) ++ ps)
              Err e -> Feed ps
          , Cmd.none
          )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
view : Model -> Html.Html Msg
view model =
  let element = case model of
        Writing p -> Views.writing Changed p
        Reading p -> Views.reading p
        Feed ps -> Views.feed ps
  in Element.layout [] <| Element.column [] [ Element.wrappedRow [] [ Element.text "Home", Element.text "Feed" ], element]
