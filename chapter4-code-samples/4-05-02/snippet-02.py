import ipaddress
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class ValidatedVpcConstruct(Construct):
    """入力値を検証するVPCのConstruct"""

    def __init__(self, scope: Construct, construct_id: str,
                 cidr: str, **kwargs):
        super().__init__(scope, construct_id)

        # 入力値のバリデーション
        self._validate_cidr(cidr)

        self.vpc = ec2.Vpc(self, "VPC",
            ip_addresses=ec2.IpAddresses.cidr(cidr),
            max_azs=2
        )

    def _validate_cidr(self, cidr: str):
        """CIDR形式の妥当性をチェック"""
        try:
            network = ipaddress.IPv4Network(cidr, strict=False)

            # 組織のポリシーに従ったチェック
            # VPCは/16〜/28の範囲しか作れないため、/16より広い
            # （prefix長が16未満の）CIDRを弾く
            if network.prefixlen < 16:
                raise ValueError(
                    f"CIDR prefix length must be >= 16 (network too wide), "
                    f"got /{network.prefixlen}"
                )

            # プライベートIPアドレス範囲のチェック
            if not network.is_private:
                raise ValueError(f"CIDR must be in private IP range, got {cidr}")

        except ipaddress.AddressValueError as e:
            raise ValueError(f"Invalid CIDR format: {cidr}") from e

# 使用例
try:
    # 正常なケース
    vpc = ValidatedVpcConstruct(self, "ValidVPC", cidr="10.0.0.0/16")

    # エラーになるケース
    invalid_vpc = ValidatedVpcConstruct(self, "InvalidVPC", cidr="8.8.8.8/24")  # パブリックIP
except ValueError as e:
    print(f"設定エラー: {e}")
