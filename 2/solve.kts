import java.io.File

enum class Move(val value: Int, val first: String, val second: String) {
    ROCK(1, "A", "X"), PAPER(2, "B", "Y"), SCISSOR(3, "C", "Z");

    companion object {
        fun fromFirst(first: String): Move = Move.values().filter { it.first == first }.first()
        fun fromSecond(second: String): Move = Move.values().filter { it.second == second }.first()

        fun calculate(opponent: Move, outcome: Outcome): Move {
            if (outcome == Outcome.DRAW) return opponent
            if (outcome == Outcome.WON) {
                return when (opponent) {
                    Move.ROCK -> Move.PAPER
                    Move.SCISSOR -> Move.ROCK
                    Move.PAPER -> Move.SCISSOR
                }
            } else if (outcome == Outcome.LOST) {
                return when (opponent) {
                    Move.ROCK -> Move.SCISSOR
                    Move.SCISSOR -> Move.PAPER
                    Move.PAPER -> Move.ROCK
                }
            }
            throw Exception("Invalid Inputs")
        }
    }
}

enum class Outcome(val value: Int, val second: String) {
    LOST(0, "X"), DRAW(3, "Y"), WON(6, "Z");

    companion object {
        fun fromSecond(second: String): Outcome = Outcome.values().filter { it.second == second }.first()

        fun calculate(opponent: Move, self: Move): Outcome {
            if (opponent == self) return DRAW
            if ((opponent == Move.ROCK && self == Move.PAPER) || (opponent == Move.PAPER && self == Move.SCISSOR) || (opponent == Move.SCISSOR && self == Move.ROCK)) return WON
            return LOST
        }
    }
}

fun first(input: List<List<String>>): Int {
    val strategies = input.map { Pair(Move.fromFirst(it[0]), Move.fromSecond(it[1])) }
    val results = strategies.map { Triple(it.first, it.second, Outcome.calculate(it.first, it.second)) }
    val value = results.map { it.second.value + it.third.value }.sum()
    return value
}

fun second(input: List<List<String>>): Int {
    val strategies = input.map { Pair(Move.fromFirst(it[0]), Outcome.fromSecond(it[1])) }
    val results = strategies.map { Triple(it.first, Move.calculate(it.first, it.second), it.second) }
    val value = results.map { it.second.value + it.third.value }.sum()
    return value
}

fun main() {
    val fileName = "./input"

    val strategies = File(fileName).readLines().map { it.split("\\W+".toRegex()) }

    println("Part 1: ${first(strategies)}")
    println("Part 2: ${second(strategies)}")

}

main()
