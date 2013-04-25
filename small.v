
Fixpoint double (n:nat) :=
  match n with
  | O => O
  | S n' => S (S (double n'))
  end.

(** **** Exercise: 2 stars (double_plus) *)
Lemma double_plus : forall n, double n = n + n .
Proof.
  intros n. induction n as [| n'].
     simpl. reflexivity.
    simpl. rewrite -> IHn'. rewrite <- plus_n_Sm.
    reflexivity. Qed.
(** [] *)
