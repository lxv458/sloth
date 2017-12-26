Contains only one file - pom.xml

The most important part:

    <dependency>
      <!-- scope is compile so all features (there is only one) are installed
      into startup.properties and the feature repo itself is not installed -->
      <groupId>org.apache.karaf.features</groupId>
      <artifactId>framework</artifactId>
      <type>kar</type>
    </dependency>