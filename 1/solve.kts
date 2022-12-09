import java.io.File

fun main() {
    val fileName = "./input"

    val lines: String = File(fileName).readText()

    val elveWeightList =
        lines.split("(?:\r?\n){2,}".toRegex()).map { s -> s.split("\r?\n".toRegex()).map { it.toInt() } }

    val elveWeight = elveWeightList.map { it.sum() }

    println("Part 1:  ${elveWeight.max()}")
    println("Part 2: ${elveWeight.sortedDescending().subList(0, 3).sum()}")

}

main()
