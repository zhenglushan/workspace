# 程序入口

JavaScript 没有预定义的入口函数，但是在 Dart 中，每个 app 都必须有一个顶级的 main() 函数作为应用程序的入口点。

```dart
// Dart
main() {
}
```



# 控制台输出

要在 Dart 中打印到控制台，可以使用 print

```dart
// JavaScript
console.log("Hello World!");

// Dart
print("Hello World!");
```

# 变量

**Dart 是类型安全的**，它使用静态类型检查和运行时的组合，检查以确保变量的值始终与变量的静态值匹配类型。

尽管类型是必需的，但是某些类型注释是可选的，因为 Dart 会执行类型推断。

## 创建和分配变量

在 JavaScript 中，无法定义变量类型。

在 Dart 中，变量必须是明确的类型或者系统能够解析、推导的类型。

```dart
// JavaScript
var name = "JavaScript";

// Dart
String name = "Dart"; // 指定变量类型为 string 类型
var otherName = "Dart"; // 推导变量类型为 string 类型
```

## 默认值

在 JavaScript 中，未初始化的变量是 undefined 。

在 Dart 中，未初始化的变量的初始值为 null。

注意：在 Dart 中，一切都是对象，所以数字也是对象，所以只要是带有数字类型的未初始化的变量的值都是 null。

```dart
// JavaScript
var name; // == undefined

// Dart
var name; // == null
int x; // == null
```

# 检查 null 或 零

在 JavaScript 中，1 或者任何非 null 对象的值都被视为 true。

```dart
// JavaScript
var myNull = null;
if(!myNull){
    console.log("null is treated as false");
}
var zero = 0;
if(!zero){
    console.log("0 is treated as false");
}
```

而在 Dart 中，只有布尔值 true 才被视为 true。

```dart
main() {
  // Dart
  var myNull = null;
  if (myNull == null) {
    print('use "== null" to check null');
  }
  var zero = 0;
  if (zero == 0) {
    print('use "== 0" to check zero');
  }
}
```



## Dart null 检查最佳实践

从 Dart 1.12 开始，null-aware 运算符可以用来帮助我们做 null 检查：

```dart
bool isConnected(a, b) {
  bool outConn = outgoing[a]?.contains(b)??false;
  bool inConn = incoming[a]?.contains(b)??false;
  return outConn || inConn;
}
```

**?.** 运算符在左边为 null 的情况下，会阻断右边的调用，**??** 运算符主要作用是在左侧表达式为 null 时，为其设置默认值。

对于表达式：

```dart
outgoing[a]?.contains(b)
```

如果 outgoing 为 null 或者 outgoing[a] 为 null 或者 contains(b) 的值为 null，都会导致表达式的值为 null。

大家看一下下面预计的执行结果：

```dart
print(null ?? false);
print(false ?? 11);
print(true ?? false);
```

使用技巧：获取一个对象中数组的长度：

```dart
searchModel ?. data ?. length ?? 0
```

# Functions

Dart 和 JavaScript 函数类似，主要区别是声明：

```dart
// JavaScript ES5
function fn(){
	return true;
}
未完
```



# 异步编程：Futures、async 和 await

