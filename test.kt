fun main() {
    println("Hello, Kotlin syntax check!")

    val user = User("Hayannoon", 29)
    println("User: ${user.name}, Age: ${user.age}")

    val numbers = listOf(1, 2, 3, 4, 5)
    val doubled = numbers.map { it * 2 }
    println("Doubled numbers: $doubled")

    greet("Kotlin")
}

data class User(val name: String, val age: Int)

fun greet(name: String) {
    println("Welcome, $name!")
}