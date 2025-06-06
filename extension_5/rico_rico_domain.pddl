(define (domain ricoRico)
  (:requirements :strips :typing :adl :equality :fluents)
  (:types
    day - object
    dish - object
    category - object
    mainCourse - dish secondCourse - dish
  )

  (:functions
    (minCalories)
    (maxCalories)
    (calories ?d - dish)

    (totalPrice)
    (price ?d - dish)
  )

  (:predicates
    (incompatible ?mc - mainCourse ?sc - secondCourse)
    (assignedMC ?d - day ?mc - mainCourse)
    (mainReady ?d - day)
    (secondReady ?d - day)
    (used ?d - dish)
    (classified ?d - dish ?c - category)
    (daySCClassif ?d - day ?c - category)
    (dayMCClassif ?d - day ?c - category)
    (dayBefore ?db - day ?d - day)
    (servedOnly ?dish - dish ?day - day)
  )

  (:action assignMC

    :parameters (?d - day ?mc - mainCourse)
    :precondition (and
      (not (mainReady ?d)) (not (used ?mc))
      (exists (?db - day ?c2 - category) (and (dayBefore ?db ?d) (secondReady ?db) (dayMCClassif ?db ?c2) (not (classified ?mc ?c2))))
      (or (servedOnly ?mc ?d) (and (not (exists (?day - day) (and (not (= ?day ?d)) (servedOnly ?mc ?day))))
        (not (exists (?mc2 - mainCourse) (and (not (= ?mc2 ?mc)) (servedOnly ?mc2 ?d))))))
    )
    :effect (and
      (used ?mc) (mainReady ?d) (assignedMC ?d ?mc) (forall (?c - category) (when (classified ?mc ?c) (dayMCClassif ?d ?c)))
    )
  )

  (:action assignSC
    :parameters (?d - day ?mc - mainCourse ?sc - secondCourse)
    :precondition (and
      (assignedMC ?d ?mc) (not (secondReady ?d)) (not (used ?sc)) (not (incompatible ?mc ?sc))
      (>= (+ (calories ?mc) (calories ?sc)) (minCalories))
      (<= (+ (calories ?mc) (calories ?sc)) (maxCalories))
      (exists (?db - day ?c2 - category) (and (dayBefore ?db ?d) (secondReady ?db) (daySCClassif ?db ?c2) (not (classified ?sc ?c2))))
      (or (servedOnly ?sc ?d) (and (not (exists (?day - day) (and (not (= ?day ?d)) (servedOnly ?sc ?day))))
        (not (exists (?sc2 - secondCourse) (and (not (= ?sc2 ?sc)) (servedOnly ?sc2 ?d))))))
    )
    :effect (and
      (used ?sc) (secondReady ?d) (increase (totalPrice) (+ (price ?mc) (price ?sc))) (forall (?c - category) (when (classified ?sc ?c) (daySCClassif ?d ?c)))
    )
  )

)
