import java.io.File

fun charSet(string: String): Set<Char> = (string.codePoints().mapToObj { c -> c.toChar() }).toList().toSet()

fun getPriority(item: Char): Int {
    var value = item.code
    when {
        value >= 97 -> value -= 96
        else -> value -= 38
    }
    return value
}

fun getSumOfPriorities(rucksack: String): Int {
    val part1 = rucksack.substring(0..(rucksack.length / 2) - 1)
    val part2 = rucksack.substring((rucksack.length / 2)..rucksack.length - 1)
    val unique1: Set<Char> = charSet(part1)
    val unique2: Set<Char> = charSet(part2)

    val commonItems: Set<Char> = unique1.intersect(unique2)

    return commonItems.map { getPriority(it) }.sum()

}

fun getSumOfBadges(rucksacks: List<String>): Int {
    var badgeSum = 0
    for (i in 0 until rucksacks.size step 3) {
        val rucksack1 = charSet(rucksacks[i])
        val rucksack2 = charSet(rucksacks[i + 1])
        val rucksack3 = charSet(rucksacks[i + 2])
        val badges = rucksack1.intersect(rucksack2).intersect(rucksack3)
        val values = badges.map { getPriority(it) }
        badgeSum += values.sum()
    }
    return badgeSum
}

fun main() {
    val fileName = "./input"

    val rucksacks = File(fileName).readLines().map { it.trim() }

    val rucksack_values = rucksacks.map { getSumOfPriorities(it) }
    val sumOfPriorities = rucksack_values.sum()

    println("Part 1: ${sumOfPriorities}")

    val sumOfBadges = getSumOfBadges(rucksacks)

    println("Part 2: ${sumOfBadges}")
}

main()
