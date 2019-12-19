module RemovingCache exposing (RemovingCache, empty, fromList, move, moves, toList)
{-| Simple Caches
You move through a list,
every time you `move` one element onto the queue, one is removed.
# RemovingCache
@docs RemovingCache

# Create
@docs empty, fromList

# Move
@docs move

# Deconstruct
@docs toList
-}

{-| A Chache, that deletes one element for each element added.
-}
type RemovingCache a = RemovingCache (List a)

{-| An empty RemovingCache is a RemovingCache with a certain length, but always the same element inside itself.
-}
empty : Int -> a -> RemovingCache a
empty length default = RemovingCache (List.repeat length default)

{-| Create a RemovingCache from an already existing list
-}
fromList : List a -> RemovingCache a
fromList = RemovingCache << List.reverse

{-| Move one element on the RemovingCache and remove one from it.
-}
move : a -> RemovingCache a -> (Maybe a,RemovingCache a)
move x (RemovingCache xs) =
  let remove_last_and_append = RemovingCache << List.reverse << List.append [x] << List.reverse
      last = List.head xs
      rest = remove_last_and_append <| case List.tail xs of
        Just a -> a
        Nothing -> []
  in (last, rest)

{-| Do [`move`](#move) multiple times over all the elements of the list.
All the elements, that are thrown out, are ignored.
-}
moves : List a -> RemovingCache a -> RemovingCache a
moves xs (RemovingCache cs) = case xs of
  [] -> RemovingCache cs
  x::rest -> moves rest (Tuple.second << move x << RemovingCache <| cs)

{-| Reverse of the [`fromList`](#fromList)
-}
toList : RemovingCache a -> List a
toList (RemovingCache xs) = List.reverse xs
