module Main exposing (..)

import Browser
import Array
import Http
import Html
import Element as E
import Element.Events as Events
import Json.Decode as D

import Post exposing ( Post )
import Views exposing ( Post_Element (..), Upload_Type (..))
import Cache exposing (Cache)

-- MAIN
main : Program () Model Msg
main = Browser.element
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  }

-- MODEL
type Main_Page
  = Reading Post
  | Writing Post
  | Feed (List Post)

type alias User = { username : String
                  , first_name : String
                  , last_name : String
                  }
type Model = Model { user : User
                   , main_page : Main_Page
                   , stored_writings : List Post -- Written posts, that are in waiting (not actually shown)
                   , stored_feed : List Post -- Fetched posts, that are not shown.
                   , stored_readings : Cache Post -- Post that have been read recently. This queue deletes one for each post added.
                   }

cache : Cache_Type -> Model -> List Post -> Model
cache ct (Model model) posts = case ct of
  Feed_Cache -> Model { model | stored_feed = posts ++ model.stored_feed }
  Writing_Cache -> Model { model | stored_writings = posts ++ model.stored_writings }
  Reading_Cache -> Model { model | stored_readings = Cache.move posts model.stored_readings }

init : flags ->  ( Model, Cmd Msg )
init _ = ( Model { user = { username = ""
                          , first_name = ""
                          , last_name = ""
                          }
                  , main_page = Feed [Post.welcome]
                  , stored_writings = []
                  , stored_feed = []
                  , stored_readings = Cache.empty 50 (Post.empty "") -- The limit may be changed as storage space increases.
                  }
                  , Post.fetch Recv_Posts )


-- UPDATE
type Msg
  = Read Post -- Switch to Reading with this Post
  | Write Post -- Writing with the Writing with this post
  | Changed  Post_Element String -- Change data structure accordingly
  | Upload Upload_Type Post
  | Saved ( Result Http.Error String )
  | Switch_To_Feed -- Go to Feed
  | Recv_Posts ( Result Http.Error (List Post) )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Read post ->
      case model.main_page of
        Writing p -> (Model {Writing p, Cmd.none )
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
              Ok new_posts -> Feed (new_posts ++ ps)
              Err error -> Feed ps
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
        Feed ps -> Views.feed Read ps
  in E.layout [] <| E.column [] [ E.wrappedRow [] [(E.el [Events.onClick Switch_To_Feed] << E.text) "Feed", (E.el [Events.onClick <| Write Post.empty] << E.text) "Write"], element]
