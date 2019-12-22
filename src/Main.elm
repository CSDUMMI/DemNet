module Main exposing (..)

import Browser
import Http
import Html
import Element as E
import Element.Events as Events
import Element.Border as Border
import Element.Input as Input
import Json.Decode as D
import EverySet exposing (EverySet)
import List.Unique as Unique

import Post exposing ( Post )
import Views exposing ( Post_Element (..), Upload_Type (..))
import RemovingCache exposing (RemovingCache)
import User exposing ( User )

-- MAIN
main : Program () Model Msg
main = Browser.element
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  }

-- MODEL
{-| State is only what is, not what might be
-}
type State
  = Reading Post User
  | Writing Post User
  | Feed (List Post) User
  | Login

{-| Storage for multiple possibilities
-}
type Storage = Storage { readings : EverySet Post
                       , writings : EverySet Post
                       , feed : List Post

{-| Reduce the State to it's bare essentialls and store it in Storage
-}
reduce : State -> Storage -> Storage
reduce state (Storage stores)
  = Storage <| case state of
      Reading p u -> EverySet.insert p stores.readings
      Writing p u -> EverySet.insert p stores.writings
      Feed ps u -> Unique.filterDuplicates (ps ++ stores.feed)
      Login -> stores
{-| Model stores for multiple possibilities.
-}
type Model
  = Model State Storage

{-| Transform a Model from one to another State saving all the important "might be"s
-}
transform : (State -> State) -> Model -> Model
transform transformer (Model old_state old_storage)
  = let new_state = transformer old_state
        new_storage = reduce new_state old_storage
    in Model new_state new_storage

init : flags ->  ( Model, Cmd Msg )
init _ = (        { user = Just
                            { username = ""
                            , first_name = ""
                            , last_name = ""
                            }
                  , main_page = Feed [Post.welcome]
                  , stored_writings = []
                  , stored_feed = []
                  , stored_readings = RemovingCache.empty 50 (Post.empty User.empty) -- The limit may be changed as storage space increases.
                  }
                  , Post.fetch Recv_Posts )


-- UPDATE
type Login_Field = Username | Password

type Msg
  = Read Post -- Switch to Reading with this Post
  | Write Post -- Writing with the Writing with this post
  | Changed  Post_Element String -- Change data structure accordingly
  | Upload Upload_Type Post
  | Saved ( Result Http.Error String )
  | Switch_To_Feed -- Go to Feed
  | Recv_Posts ( Result Http.Error (List Post) )
  | Login_Change Login_Field String
  | Login_Request

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Read post ->
      let new_main_page = change_main_page <| Reading post
      in case model.main_page of
        Writing p ->  ( new_main_page <| cache_writings model [p],  Cmd.none )
        Reading p ->  ( new_main_page <| cache_readings model [p], Cmd.none )
        Feed ps ->    ( new_main_page <| cache_feed model ps, Cmd.none )
    Write post ->
      let new_main_page = change_main_page <| Writing post
      in case model.main_page of
        Writing p -> ( new_main_page <| cache_writings model [p], Cmd.none )
        Reading p -> ( new_main_page <| cache_readings model [p], Cmd.none )
        Feed ps -> ( new_main_page <| cache_feed model ps, Cmd.none )

    Changed element post_element ->
      let (new_main_page, cmd) = case model.main_page of
            Writing p ->
              let post = case element of
                    Title -> { p | title = post_element, saved = False }
                    Content -> { p | content = post_element, saved = False }
              in ( Writing post, Cmd.none )
            Reading p -> ( Reading p, Cmd.none )
            Feed ps -> ( Feed ps, Cmd.none )
      in (change_main_page new_main_page model, cmd)

    Upload kind post ->
      let cmd = case kind of
            Publish -> Post.publish Saved post
            Save -> Post.save Saved post
          new_feed = if kind == Publish then post::model.stored_feed else model.stored_feed
      in ({ model | stored_feed = new_feed }, cmd)

    Saved result ->
      let (new_main_page, cmd) = case model.main_page of
            Writing p -> case result of
              Ok response -> ( Writing { p | saved = ( response == "Posted" ) }, Cmd.none )
              Err err -> ( Writing { p | saved = False }, Cmd.none )
            Reading p -> ( Reading p, Cmd.none )
            Feed ps -> ( Feed ps, Cmd.none )
      in (change_main_page new_main_page model, cmd)

    Switch_To_Feed ->
      let (new_main_page, cmd) = case model.main_page of
            Writing p -> case p.saved of
              True -> ( Feed model.stored_feed, Post.fetch Recv_Posts )
              False -> ( Writing p, Post.save Saved p )
            Reading p -> ( Feed model.stored_feed, Post.fetch Recv_Posts )
            Feed ps   ->  ( Feed ps, Post.fetch Recv_Posts )
      in (change_main_page new_main_page model, cmd)

    Recv_Posts posts ->
      let (new_main_page, cmd) = case model.main_page of
            Writing p -> ( Writing p, Cmd.none )
            Reading p -> ( Reading p, Cmd.none )
            Feed ps   ->
              ( case posts of
                  Ok new_posts -> Feed (new_posts ++ ps)
                  Err error -> Feed ps
              , Cmd.none
              )
      in (change_main_page new_main_page model, cmd)

    Login_Change field input ->
      let new_main_page = change_main_page <| Login <| Post.empty <| User.empty
      in case model.main_page of
            Writing p -> new_main_page <| cache_writings model [p], Cmd.none)
            Reading p -> new_main_page <| cache_readings model [p], Cmd.none)
            Feed ps   -> new_main_page <| cache_feed model ps, Cmd.none)

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- VIEW
view : Model -> Html.Html Msg
view model =
  let element = case model.main_page of
        Writing p -> Views.writing Changed (Upload) p
        Reading p -> Views.reading p
        Feed ps -> Views.feed Read ps
        Login user ->
              E.column []
                [ Input.username [] { onChange = Login_Change Username, text = "Username", placeholder = Nothing, label = Input.labelLeft [] <| E.text "Username:" }
                , Input.currentPassword [] { onChange = Login_Change Password, text ="Password", placeholder = Nothing, label = Input.labelLeft [] <| E.text "Password:", show = False }
                , Input.button [] { onPress = Just Login_Request, label = E.text "Login" }
                ]
  in E.layout [E.centerX]
      <| E.column [] [element]
