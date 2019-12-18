module Cache exposing (Cache, empty, fromList, move, moves, toList)
{-| Simple Cache
You move through a list,
every time you `move` one element onto the queue, one is removed.
# Definition
@docs Cache

# Create
@docs empty, fromList

# Move
@docs move

# Deconstruct
@docs toList
-}

{-| Cache uses a List under the hood
-}
type Cache a = Cache (List a)

{-| An empty Cache is a Cache with a certain length, but always the same element inside itself.
-}
empty : Int -> a -> Cache a
empty length default = Cache (List.repeat length default)

{-| Create a Cache from an already existing list
-}
fromList : List a -> Cache a
fromList = Cache << List.reverse

{-| Move one element on the Cache and remove one from it.
-}
move : a -> Cache a -> (Maybe a,Cache a)
move x (Cache xs) =
  let remove_last_and_append = Cache << List.reverse << List.append [x] << List.reverse
      last = List.head xs
      rest = remove_last_and_append <| case List.tail xs of
        Just a -> a
        Nothing -> []
  in (last, rest)

{-| Do [`move`](#move) multiple times over all the elements of the list.
All the elements, that are thrown out, are ignored.
-}
moves : List a -> Cache a -> Cache a
moves xs (Cache cs) = case xs of
  [] -> Cache cs
  x:rest -> moves rest (Tuple.second << move x << Cache <| cs)

{-| Reverse of the [`fromList`](#fromList)
-}
toList : Cache a -> List a
toList (Cache xs) = List.reverse xs
