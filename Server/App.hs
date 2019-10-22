module App where

data GlobalConfig = GlobalConfig { static :: String }

data Cmd =
    None
  | Repond Response

data Config = Config  { globalConfig :: GlobalConfig
                      , userConfig :: Model
                      , respond :: Msg -> Model -> ( Model, Cmd )
                      }


app :: Config -> IO ()
app Config  { globalConfig = globalConfig
            , userConfig = userConfig
            , respond = respond
            } = do
              respond 
