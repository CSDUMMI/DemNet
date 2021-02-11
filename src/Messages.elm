module Messages exposing  ( decoder
                          , encoder
                          , publish
                          , save
                          , request_one
                          , request_many
                          )

import Json.Decode as D
import Json.Encode as E

type alias Message
  = { from : User
    , to : User
    , title : String
    , content : String
    }


decoder : D.Decoder Message
decoder =
  D.map4 Message
    (D.field "from" D.string)
    (D.field "to"  <| D.list D.string)
    (D.at ["body", "title"] D.string)
    (D.at ["body", "content"] D.string)

encode : Message -> E.Value
encode message =
  E.object []
