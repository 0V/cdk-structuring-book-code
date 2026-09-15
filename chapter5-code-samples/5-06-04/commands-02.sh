# セキュリティグループの変更例
[~] AWS::EC2::SecurityGroup MySecurityGroup
 └─ [~] SecurityGroupIngress
     └─ [+] {"IpProtocol":"tcp","FromPort":443,"ToPort":443,"CidrIp":"0.0.0.0/0"}
