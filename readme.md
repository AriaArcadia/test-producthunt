整个爬虫程序依靠`DrissionPage`模拟浏览器来绕过cf盾，最终实现launches的获取

- 可以适当增加`time.sleep`的时间，防止被ban ip
- API采用GraphQL构建，因此请求链接中，`sha256Hash`不需要在意，是网站为了降低运行负担的手段

### 第一步

主要是`huntcat.py`，还没写完凑合着用

获取https://www.producthunt.com/categories内所有子项（例如AI notetakers，共227项）的链接，得到（项目链接-项目名称），

- 可以通过在[该网页](https://www.producthunt.com/categories)网页控制台选择selector

  - ```javascript
    // 直接查找符合条件的a标签
    const links = document.querySelectorAll('.flex.flex-col.gap-3 a[href*="/categories/"]');
    
    // 提取并输出href
    const hrefs = Array.from(links).map(link => link.href);
    console.log(hrefs);
    console.log(`找到 ${hrefs.length} 个符合条件的链接`);
    
    // 详细输出
    links.forEach((link, index) => {
        console.log(`${index + 1}. ${link.href}`);
    });
    ```

- 也可以通过ProductCategoriesPage，

  ```url
  https://www.producthunt.com/frontend/graphql?operationName=ProductCategoriesPage&variables={"cursor":null}&extensions={"persistedQuery":{"version":1,"sha256Hash":"efee7f452f3db3f6a234e4970291b6c502057bd1368af4b4837e56bd1c4baac4"}}
  ```
  参数表
  ```json
  {
  	"cursor":“null”或者“MTA”
  }
  ```

- 得到22个大类，227个小类，（保存在`items.json`）

执行获取`huntcat.py`，得到（项目链接-项目名称-app数-页数）

- 可以通过网页保存和文字定位，有些页面比较奇怪，获取信息不太全

- 也通过首页链接CategoryPageQuery

  ```
  https://www.producthunt.com/frontend/graphql?operationName=CategoryPageQuery&variables={"slug":"ai-meeting-notetakers","path":"/categories/ai-meeting-notetakers"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"af541f9180b594284c2ded4818df1357f2d773cf5edd9d1fd6684cf8f7353e51"}
  ```
  
  参数表
  
  ```json
  {
  	"slug":"ai-meeting-notetakers",
      "path":"/categories/ai-meeting-notetakers"
  }
  ```
  
- 得到项目app数（totalCount属性），总页数

- 通过简单的json处理得到（`列表页（1层）.xls`）


### 第二步

主要是`hunt.py`

遍历项目链接，得到app列表。输入上面获得的每个项目链接和最大页数

- 通过CategoryPageListQuery

  ```
  https://www.producthunt.com/frontend/graphql?operationName=CategoryPageListQuery&variables={"featuredOnly":true,"slug":"ai-meeting-notetakers","order":"highest_rated","page":2,"pageSize":15,"tags":null}&extensions={"persistedQuery":{"version":1,"sha256Hash":"286726a8f1e788ece1f7214488cecd46e64b244ff190934bfa043ee14e5c106d"}}
  ```

  参数

  ```
  {
  	"featuredOnly":true,
  	"slug":"ai-meeting-notetakers",
  	"order":"highest_rated",
  	"page":2,
  	"pageSize":15,
  	"tags":null
  }
  ```
  
- 得到大量json文件，获取json文件的内容，执行批处理程序`json2xls.py`，生成（app名-launches数）



### 第三步

主要是`huntlaunch.py`

遍历app的launch页面，获得launch详细信息

- 通过ProductPageLaunches

  ```
  https://www.producthunt.com/frontend/graphql?operationName=ProductPageLaunches&variables={"slug":"notion","cursor":"MTA","order":"DATES"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"b6d9a2df9579eeada897cd06824673aecd21ebfb5fa4bb99ab4e651574e4d0ae"}}
  ```

  参数

  ```
  {
  	"slug":"notion",
  	"cursor":"null"或"MTA"或"MjA",
  	"order":"DATES"
  }
  ```

- 得到大量launches数据

- 使用批处理程序进行提取，可以交给AI，提示词类似下面的：

  ```
  写一个python程序，遍历工作目录（./launches/）下所有json文件，并写入实例（第三层）.xls文件。具体要求如下：
  1. 对于每一个json文件
  1.1 获取data->productCategory->slug的属性，记为A，获取data->productCategory-path属性，记为B
  1.2 对于data->productCategory->products->edges下的每一个大括号包裹的元素
  1.2.1 获取node->name属性记为C，获取node->postsCount属性记为D，获取node->slug属性记为E
  1.2.2 写入一行A,B,C,D,E到output.xls
  我已经能保证给出的json文件符合要求
  ```

  

  

  

