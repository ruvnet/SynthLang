---
title: Category Theory Concepts
domain: mathematics
category: Category Theory
overview: Abstract mathematical framework dealing with mathematical structures and relationships between them.
---

# Basic Definitions
C = (Ob(C), hom(C), ∘)
F: C → D (Functor)

# Natural Transformations
η: F ⇒ G
∀X∈Ob(C): ηX: F(X) → G(X)

# Universal Properties
Initial Object: ∀X∃!f:I→X
Terminal Object: ∀X∃!f:X→T

# Adjunctions
F ⊣ G
Hom(F(A),B) ≅ Hom(A,G(B))