module Messages exposing ( message_decoder
                        , message_encoder
                        , publish
                        , save
                        , request_message
                        , request_messages
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
