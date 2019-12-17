module Queue exposing (Queue, empty, fromList, move, toList)
{-| Simple Queue
You move through a list,
every time you `move` one element onto the queue, one is removed.
# Definition
@docs Queue

# Create
@docs empty, fromList

# Move
@docs move

# Deconstruct
@docs toList
-}

{-| Queue uses a List under the hood
-}
type Queue a = Queue (List a)

{-| An empty Queue is a Queue with a certain length, but always the same element inside itself.
-}
empty : a -> Int -> Queue a
empty default length = Queue (List.repeat length default)

{-| Create a Queue from an already existing list
-}
fromList : List a -> Queue a
fromList = Queue << List.reverse

{-| Move one element on the Queue and remove one from it.
-}
move : a -> Queue a -> (Maybe a,Queue a)
move x (Queue xs) =
  let remove_last_and_append = Queue << List.reverse << List.append [x] << List.reverse
      last = List.head xs
      rest = remove_last_and_append <| case List.tail xs of
        Just a -> a
        Nothing -> []
  in (last, rest)

{-| Reverse of the [`fromList`](#fromList)
-}
toList : Queue a -> List a
toList (Queue xs) = List.reverse xs
