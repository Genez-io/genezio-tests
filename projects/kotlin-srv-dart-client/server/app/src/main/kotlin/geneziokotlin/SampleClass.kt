package geneziokotlin

import kotlinx.serialization.Serializable

@Serializable
data class Point(
    val x: Int,
    val y: Int,
)

@Serializable
data class TestResult(
    val number: Int,
    val string: String,
    val point: Point,
)

@Serializable
data class ComplicatedClass(
    val a: Point,
    val b: Point,
    val otherPoints: List<Point>,
    val pointsMap: Map<String, List<Point>>,
    val pointsMap2: List<List<Map<String, List<Point>>>>,
)

class HelloWorldService {
    var methodWithVoidReturnVoidCount = 0
    var methodWithStringReturnVoidParam = ""
    var methodWithPointReturnVoidParam = Point(0, 0)

    fun methodWithVoidReturnVoid() {
        methodWithVoidReturnVoidCount = 100
    }

    fun methodWithStringReturnVoid(string: String) {
        this.methodWithStringReturnVoidParam = string
    }

    fun methodWithPointReturnVoid(point: Point) {
        this.methodWithPointReturnVoidParam = point
    }

    fun methodWithReturnSimpleString(test: String): String {
        return "hello: " + test
    }

    fun methodWithReturnSimpleInt(test: Int): Int {
        return (42 + test)
    }

    fun methodWithReturnSimpleBool(): Boolean {
        return true
    }

    fun replacePointsInArray(list: List<Point>): List<Point> {
        return listOf(
            Point(list[0].x + 10, list[0].y + 10),
            Point(list[1].x + 10, list[1].y + 10),
            Point(list[2].x + 10, list[2].y + 10)
        )
    }

    fun replacePointsInMap(map: Map<String, Point>): Map<String, Point> {
        return mapOf(
            "hello" to Point(map["hello"]!!.x, map["hello"]!!.y)
        )
    }

    fun getNumbers(x: Int, y: Int, z: Int): List<Int> {
        return listOf(x, y, z)
    }

    fun getStrings(x: String, y: String, z: String): List<String> {
        return listOf(x, y, z)
    }

    fun getPoints(x: Int, y: Int, count: Int): List<Point> {
        var list = mutableListOf<Point>()
        for (i in 0..count) {
            list.add(Point(x * i, y * i))
        }
        return list
    }

    fun getTestResult(): TestResult {
        return TestResult(
            this.methodWithVoidReturnVoidCount,
            this.methodWithStringReturnVoidParam,
            this.methodWithPointReturnVoidParam,
        )
    }

    fun getComplicatedClass(x: Int, y: Int): ComplicatedClass {
        return ComplicatedClass(
            Point(x, y),
            Point(x, y),
            listOf(Point(x * 10, y * 10), Point(x * 100, y * 100)),
            mapOf(
                "a" to listOf(Point(x * 1000, y * 1000), Point(x * 1000, y * 1000)),
                "b" to listOf(Point(x * 10000, y * 10000), Point(x * 10000, y * 10000))
                ),
            listOf(
                listOf(
                    mapOf(
                        "a" to listOf(Point(x * 20, y * 20), Point(x * 20, y * 20)),
                        "b" to listOf(Point(x * 30, y * 30), Point(x * 30, y * 30))
                    )
                )
            )
            )
        }
}
